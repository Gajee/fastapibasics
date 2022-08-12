from fastapi import FastAPI, Request, Form, Response, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from fastapi.middleware.cors import CORSMiddleware

# from starlette import status
# from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
# from starlette.requests import Request
# from starlette.responses import Response
# from starlette.types import ASGIApp


from routes.index import route
from fastapi.staticfiles import StaticFiles
import pandas as pd  

# class LimitUploadSize(BaseHTTPMiddleware):
#     def __init__(self, app: ASGIApp, max_upload_size: int) -> None:
#         super().__init__(app)
#         self.max_upload_size = max_upload_size

#     async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
#         if request.method == 'POST':
#             if 'content-length' not in request.headers:
#                 return Response(status_code=status.HTTP_411_LENGTH_REQUIRED)
#             content_length = int(request.headers['content-length'])
#             if content_length > self.max_upload_size:
#                 return Response(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)
#         return await call_next(request)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")



origins = ["*"]
methods = ["*"]

app.add_middleware(
    CORSMiddleware,
    
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=["*"],
    
)
# app.add_middleware(
#         LimitUploadSize, max_upload_size=1024
# )




app.include_router(route)





# from starlette_validation_uploadfile import ValidateUploadFileMiddleware



# app = FastAPI()

# app.add_middleware(
#         LimitUploadSize, max_upload_size=1024
# )

# @app.post("/upload")
# def upload_file(request: Request, file: UploadFile = File(...)):
#     form = request.form()
#     # content_type = form[next(iter(form))].content_type

#     size = request.headers["content-length"]

#     df1 = pd.read_csv(file.file)
#     file_location = f"static/uploads/{file.filename}"
#     df1.to_csv(file_location, index=False)

#     return {
#         "filename": file.filename,
#         # "content_type": content_type,
#         "file_size": size
#     }