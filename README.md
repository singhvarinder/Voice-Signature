# Voice Signature
A simple Voice Signature (Authentication) system using pre-trained Convolutional Neural Network.

Features:

## Enrollment:
Register a new user using an audio file of his/her voice
/
## Recognition:
Authenticate a user if it matches voice prints with stored registred voice

## Required:
Download weights from the official pop2piano repository
https://huggingface.co/sweetcocoa/pop2piano/blob/main/model-1999-val_0.67311615.ckpt
Save above fiel in root director where app.py is stored

## API Endpoints :
- app.py : Entry point of mail Rest API endpoint below are endpoints
  - / : Get uploaded file list
  - /upload : To upload voice files to recognize and display in main page list
  - /record/<userName> : To record user voice and add in recorded database
  - /recognize/<userName>' : To recognize recorded user voice
  - /static/action/<userName> : To play listed user voice and recognize voice for demo

> index.html : Demo web page using app.py Rest API calls to register/recognize the sample calls
> Voices can be "UPLOADED" to recognize and can be "RECORDED" to register user voices 

## For Develpers - Creating a Virtual Environment:
- Create virtual env
> python -m venv env
- Activate virtual enviorment
> source env/bin/activate - For macOS/Linux <br>
>.\env\Scripts\activate - For Windows


