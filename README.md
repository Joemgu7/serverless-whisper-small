# 🍌 Banana Whisper Small++

This is the ultimate production ready deployment of Whisper. It uses a custom build of Whisper, which is based on the latest Whisper release, but with a few modifications to make it run 10-20% faster than the stock whisper, without sacrificing quality of transcription 🤯

It also has added flexibility, it can accept more parameters than the stock Whisper templates out there:

- `base64String` - The base64 encoded audio file
- `format` - The format of the audio file. Defaults to `mp3`
- `kwargs` - A JSON string of additional arguments to pass to whisper.transcribe(). Defaults to `{}`. See the Whisper documentation for more information on the available arguments.

It not only returns the text in the result, but also segment information and language information.

## 🚀 Getting Started

On the client, call the model like so:

```
import banana_dev as banana
import ffmpeg
import base64

# read audio from video/audio and convert to opus with 16k sampling rate, mono channel, 48k bitrate, loglevel error

input_path = "input.mp4"

try:
  out, _ = (
      ffmpeg
      .input(input_path)
      .output('-', format='opus', acodec='libopus', ac=1, ar='16k', b='48k', loglevel='error')
      .run(cmd=['ffmpeg', '-nostdin'], capture_stdout=True, capture_stderr=True)
  )
except Exception as e:
  raise RuntimeError(f"Failed to load audio: {e.stderr.decode()}") from e


# HERE THE MAGIC HAPPENS

opus_bytes_base64 = base64.b64encode(out).decode("ISO-8859-1")

model_inputs = {
  "base64String": opus_bytes_base64,
  "format": "opus",
  "kwargs": {
    "beam_size": 4,
    "temperature": [0.0, 0.2, 0.7],
  }
}

api_key = "YOUR_API_KEY"
model_key = "YOUR_MODEL_KEY"


out = banana.run(api_key, model_key, model_inputs)
result = out["modelOutputs"][0]

# Use the result just as the standard whisper model output
```
