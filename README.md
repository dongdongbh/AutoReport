## AutoLogin

AutoLogin is a web login script supporting multiple users. It adopt LSTM to read captcha for login. In many web crawler situation, login is required, so I wrote this demo for reference. It tested on [GZHU](https://cas.gzhu.edu.cn/cas_server/login) login system.

## Requirements 

### Install requirements
Here, I want to make the captcha recognition more accurate, so the pre-process besed on opencv and numpy is incorporated, If you do not want that, just remove related codes, then there is no need to install these packages.
```
pip install requests bs4 pillow pytesseract tesseract opencv numpy lxml
```


## Quick start
You may have to modify the code for your website

1. do Install-requirements in last section

2. clone code

3. modify user info in `arg.json`

## Fit the code for your own website
1. modify `login_url` and `captcha_url` in  `arg.json`
2. check login POST request parameters packing on your website
3. check captcha requirements and modify the code accordingly

## Acknowledgement
[Tesseract](https://nanonets.com/blog/ocr-with-tesseract/#preprocessingfortesseract?&utm_source=nanonets.com/blog/&utm_medium=blog&utm_content=%5BTutorial%5D%20OCR%20in%20Python%20with%20Tesseract,%20OpenCV%20and%20Pytesseract) is an open source text recognition (OCR) Engine.  Tesseract developed from OCRopus model in Python which was a fork of a LSTM in C++, called CLSTM. CLSTM is an implementation of the LSTM recurrent neural network model in C++, using the Eigen library for numerical computations.

You can train and fine-tune the model by following [this](https://github.com/tesseract-ocr/tessdoc/blob/master/TrainingTesseract-4.00.md).

