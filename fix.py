"""
Sometimes Ableton Live will create a .wav file with a 0-byte header. This script will fix the header so the file can be played.
Usage: fix.py <file_path>

Write the 36-byte .wav file header to the file if the first 36 bytes are all 0x00
Assumes 2-channel, 44100 Hz, 16-bit PCM
"""
import os
import sys

def fix_wav_header(file_path):
    with open(file_path, 'rb+') as f:
        header = f.read(36)
        if header == b'\x00'*36:
            file_size = os.path.getsize(file_path)
            # RIFF header: 4 bytes
            data = b'RIFF'
            # File size - 8 bytes: 4 bytes
            fs = (file_size - 8).to_bytes(4, byteorder='little')
            # WAVEfmt header: 8 bytes
            wavefmt = b'WAVEfmt '
            # Size of fmt chunk: 4 bytes
            chunk = b'\x10\x00\x00\x00'
            # PCM format: 2 bytes
            pcm = b'\x01\x00'
            # 2 channels: 
            ch = b'\x02\x00'
            # 44100 Hz: 4 bytes
            samplerate = b'\x44\xAC\x00\x00'
            # 264600 bytes per second: 4 bytes
            rate = b'\x98\x09\x04\x00'
            # 6 bytes per sample: 2 bytes
            bytes_per_sample = b'\x06\x00'
            # 18 bits per sample: 2 bytes
            bps = b'\x18\x00'
            # data header: 4 bytes
            data_hdr = b'data'
            # Data size: 4 bytes
            data_size = (file_size - 44).to_bytes(4, byteorder='little')
            f.seek(0)
            # Write a total of 44 bytes
            f.write(data + fs + wavefmt + chunk + pcm + ch + samplerate + rate + bytes_per_sample + bps + data_hdr + data_size)
            print(f'Fixed {file_path}')
        else:
            print(f'Header is not all 0x00 for {file_path}')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python fix.py <file_path>')
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.exists(file_path):
        print(f'File not found: {file_path}')
        sys.exit(1)

    # Duplicate a backup copy of the file
    print('================== WARNING ==================\n')
    input('WARNING: This will overwrite the file. MAKE SURE YOU HAVE A BACKUP. Press Enter to continue or Ctrl+C to cancel.')
    fix_wav_header(file_path)
