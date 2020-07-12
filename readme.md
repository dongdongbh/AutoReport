AutoReport is a web reporting script supporting multiple users. It use LSTM to read captcha for login.

## Requirements 

### Basic
* python 3

### For web access
* selenium
* chromedriver

### For captcha code
* pillow
* pytesseract and tesseract
* opencv

### Install requirements
Here, I want to make the captcha recognition more accurate, so the pre-process besed on opencv and numpy is incorporated, If you do not want that, just remove related codes, then there is no need to install these packages.
1. download [chromedriver](https://chromedriver.chromium.org/downloads/version-selection) and add it to path 
2. install python packages
```
pip install selenium pillow pytesseract tesseract opencv numpy 
```


## Quick start
You may have to modify the code for your website

1. do Install-requirements in last section

2. clone code

3. modify user info in `arg.json`

4. set up task scheduler

   for Linux user run `crontab -e`, add

   ```
   0 8 * * * python3 AutoReport.py
   ```

   then it will report at 8:00 am everyday.


## Fit the code for your own website
1. modify `login_url` and `report_url` in  `arg.json`
2. check elements location, including username, password, captcha, login_button, submit_button, etc., and modify the code.
3. check captcha requirements and modify the code accordingly
4. check post workflow match your report system

## Acknowledgement
[Tesseract](https://nanonets.com/blog/ocr-with-tesseract/#preprocessingfortesseract?&utm_source=nanonets.com/blog/&utm_medium=blog&utm_content=%5BTutorial%5D%20OCR%20in%20Python%20with%20Tesseract,%20OpenCV%20and%20Pytesseract) is an open source text recognition (OCR) Engine. 

Tesseract developed from OCRopus model in Python which was a fork of a LSMT in C++, called CLSTM. CLSTM is an implementation of the LSTM recurrent neural network model in C++, using the Eigen library for numerical computations.

You can train and fine-tune the model by following [this](https://github.com/tesseract-ocr/tessdoc/blob/master/TrainingTesseract-4.00.md).