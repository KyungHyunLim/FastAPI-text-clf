from typing import Optional, List

from fastapi import FastAPI, HTTPException
from fastapi.param_functions import Depends
from pydantic.main import BaseModel

from typing import *
from model import get_model, get_tokenizer, predict_from_text

from pydantic import Field

from transformers import AutoModelForSequenceClassification, AutoTokenizer

app = FastAPI()

predicts = []
model = None

class Comments(BaseModel):
    text: str = Field(default=str)
    label: str = Field(default=str)

@app.on_event("startup")
def init():
    global model
    if model is None:
        model = get_model()

@app.get("/")
def hello_world():
    return {"악성 댓글": "분류해보자!"}

@app.post("/inference", description="댓글의 악성 여부를 판단합니다.")
async def make_inference(text: str,
                     #model: AutoModelForSequenceClassification = Depends(get_model),
                     tokenizer: AutoTokenizer = Depends(get_tokenizer)):
 
    try:
        inference_result = predict_from_text(model=model, tokenizer=tokenizer, text=text)
    except:
        raise HTTPException(status_code=404, detail=f"예측과정에서 오류가 발생했습니다. [text: {text}]")

    new_conmments = Comments()
    new_conmments.text = text
    new_conmments.label = inference_result
    predicts.append(new_conmments)

    return new_conmments

@app.get("/results", description="댓글 판별 리스트를 가져옵니다")
async def get_Comments() -> List[Comments]:
    return predicts

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
