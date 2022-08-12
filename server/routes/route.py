from fastapi import APIRouter, Form, UploadFile, File, Depends, Response, status,Request

from typing import List, Union, Optional
from config.db import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from controllers.upload import upload_files
import pprint
import pdfkit
import PyPDF2 
route = APIRouter()



@route.post('/upload', status_code = 200)
async def upload_file(request: Request, name: str = Form(default=None), last: str = Form(default=None), phone: str = Form(default=None), file: Union[UploadFile, str] = File(None)):
    max_upload_size = 10000
    print(file.headers)
    file_type = file.headers['content-type']
    mylist = ["text/csv"]
    if name == None and last == None and phone == None and file == "undefined":
        print("hhhhh")
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': False, 'description' : "form fileds name, last and phone are required filed"}
    content_length = int(request.headers['content-length'])

    if content_length > max_upload_size:
        return {'status': False, 'description' :"file is too large"}
    
    if file_type not in mylist:
        return {'status': False, 'description' :"file is not csv"}
    
    thisdict = {"name": name, "last": last, "phone": phone}
    return upload_files.upload(thisdict, file)


@route.post('/import', status_code = 200)
def c_import(name: str = Form(default=None), ba: str = Form(default=None), email: str = Form(default=None), c_info: str = Form(default=None), file: str = Form(default=None), db: Session = Depends(get_db)):
    if name == None and ba == None and email == None and c_info == None:
        Response.status_code = status.HTTP_404_NOT_FOUND
        return {'status': False, 'description' : "form fileds are required filed"}
    thisdict = [ name, ba,  email, c_info]
    return upload_files.cli_import(thisdict, file, email, db=db)
    # return "nnn"

@route.post('/checking')
async def checking():
    pdfkit.from_file('static/uploads/TEMPLATE2.html', 'static/uploads/out.pdf')

@route.post('/getcontent')
def getcontent():
    # creating a pdf file object 
    pdfFileObj = open('static/uploads/out.pdf', 'rb') 
        
    # creating a pdf reader object 
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
        
    # printing number of pages in pdf file 
    print(pdfReader.numPages) 
        
    # creating a page object 
    pageObj = pdfReader.getPage(0) 
        
    # extracting text from page 
    stri = pageObj.extractText()
    print(type(stri)) 
        
    # closing the pdf file object 
    pdfFileObj.close() 

