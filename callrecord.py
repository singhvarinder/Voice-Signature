import pyaudio
import wave
import soundfile as sf


def recordcall():
    # Audio configuration
    lFORMAT = pyaudio.paInt16  # Audio format (16-bit)
    lCHANNELS = 1  # Number of channels (1 for mono, 2 for stereo)
    lRATE = 44100  # Sampling rate (44.1 kHz)
    lCHUNK = 1024  # Buffer size (number of samples per chunk)
    lRECORD_SECONDS = 5  # Duration to record in seconds
    lOUTPUT_FILENAME = "uploads/sample.flac"  # Output filename

    # Initialize PyAudio
    laudio = pyaudio.PyAudio()

    # Open stream
    lstream = laudio.open(format=lFORMAT,
                          channels=lCHANNELS,
                          rate=lRATE,
                          input=True,
                          frames_per_buffer=lCHUNK)

    print("Recording...")

    # Record audio
    lframes = []
    for i in range(0, int(lRATE / lCHUNK * lRECORD_SECONDS)):
        ldata = lstream.read(lCHUNK)
        lframes.append(ldata)

    print("Finished recording.")

    # Stop and close the stream
    lstream.stop_stream()
    lstream.close()
    laudio.terminate()

    # Save the recorded data as a WAV file
    lwave_output_filename = "output.wav"
    lwf = wave.open(lwave_output_filename, 'wb')
    lwf.setnchannels(lCHANNELS)
    lwf.setsampwidth(laudio.get_sample_size(lFORMAT))
    lwf.setframerate(lRATE)
    lwf.writeframes(b''.join(lframes))
    lwf.close()

    # Convert WAV to FLAC
    ldata, samplerate = sf.read(lwave_output_filename)
    sf.write(lOUTPUT_FILENAME, ldata, samplerate, format='FLAC')

    print(f"Audio saved as {lOUTPUT_FILENAME}")

