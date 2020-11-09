def transcribe_file(speech_file):
    """Transcribe the given audio file."""
    from google.cloud import speech
    import io
    import os

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountKey.json'

    client = speech.SpeechClient()

    with io.open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.AMR,
        sample_rate_hertz=8000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    recognized_text = ''

    for result in response.results:
        recognized_text = result.alternatives[0].transcript

    return recognized_text.lower()

