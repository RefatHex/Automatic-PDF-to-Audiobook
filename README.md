# Audiobook Generator

This project is a simple Audiobook Generator built using Python and Streamlit. It allows users to upload a PDF file, which is then converted into an audio file, providing an easy way to listen to the contents of the PDF.

## Technologies Used

- **Python**: The primary programming language used for development.
- **Streamlit**: A Python library used for creating interactive web applications with simple Python scripts.
- **Tika**: A Python library for extracting text content from PDF files.
- **MoviePy**: A Python library for video editing, which is used here for audio manipulation.
- **Edge TTS**: A text-to-speech (TTS) library for Python, providing various voices for generating audio from text.

## How it Works

1. **Upload PDF**: Users can upload a PDF file containing the text they want to convert into an audiobook.
2. **Text Extraction**: The PDF file is processed using the Tika library to extract the text content.
3. **Text-to-Speech Conversion**: The extracted text is divided into smaller chunks, and for each chunk, audio is generated using the Edge TTS library. Multiple voices can be selected for generating diverse audio.
4. **Audio Concatenation**: The generated audio clips are concatenated together to form a single audio file.
5. **Download**: The final audio file is made available for download.

## Contribution

Contributions to this project are welcome and encouraged. If you'd like to contribute, you can do so by:

- Improving the user interface for a better user experience.
- Adding support for more file formats besides PDF.
- Optimizing the audio generation process for faster performance.
- Fixing any bugs or issues present in the current implementation.

To contribute, simply fork this repository, make your changes, and submit a pull request. Your contributions will be greatly appreciated!

Feel free to reach out if you have any questions or suggestions for this project. Happy coding!
