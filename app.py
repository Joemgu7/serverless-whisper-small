import whisper
import os
import base64
from io import BytesIO

# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"
def init():
    global model
    model_name = os.getenv("MODEL_NAME")
    model = whisper.load_model(model_name, device="cuda", in_memory=True, fp16=True)

def _parse_arg(args : str, data : dict, default = None, required = False):
    arg = data.get(args, None)
    if arg == None:
        if required:
            raise Exception(f"Missing required argument: {args}")
        else:
            return default

    return arg

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(model_inputs:dict) -> dict:
    global model

    # Parse out your arguments
    try:
        BytesString = _parse_arg("base64String", model_inputs, required=True)
        format = _parse_arg("format", model_inputs, "mp3")
        kwargs = _parse_arg("kwargs", model_inputs, {})
        if format not in ["opus", "wav", "flac", "mp3", "m4a"]:
            raise Exception(f"Invalid format: {format}")

    except Exception as e:
        return {"error":str(e)}
    
    bytes = BytesIO(base64.b64decode(BytesString.encode("ISO-8859-1")))

    tmp_file = "input."+format
    with open(tmp_file,'wb') as file:
        file.write(bytes.getbuffer())
    
    # Run the model
    result = model.transcribe(tmp_file, fp16=True, **kwargs)
    result['segments'] = [{
        "id":x['id'],
        "seek":x['seek'],
        "start":x['start'],
        "end":x['end'],
        "text":x['text']
        } for x in result['segments']]
    os.remove(tmp_file)
    # Return the results as a dictionary
    return result
