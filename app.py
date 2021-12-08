from typing import Optional, List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Model(BaseModel):
    id: int
    name: str
    version: str
    description: Optional[str]
    tags: List[str]
    artifact_url: str

models: List[Model] = []

class CreateModelIn(BaseModel):
    name: str
    version: str
    description: Optional[str]
    tags: List[str]
    artifact_url: str

class CreateModelOut(BaseModel):
    id: int

class UpdateModelIn(BaseModel):
    version: str
    description: Optional[str]
    tags: List[str]
    artifact_url: str

class UpdateModelOut(BaseModel):
    version: str
    description: Optional[str]
    tags: List[str]
    artifact_url: str

@app.get("/models")
def get_models():
    # model 리스트를 리턴합니다
    return models

@app.get("/model/{model_id}")
def get_model(model_id: int):
    # model 리스트로 부터 model_id가 일치하는 model을 가져와 리턴합니다
    for model in models:
        if model.id == model_id:
            return model
    # model_id가 없을 때 404 에러와 에러 메시지를 출력합니다
    raise HTTPException(status_code=404, detail=f"모델을 찾을 수 없습니다 [id: {model_id}]")

@app.get("/model")
def get_model_by_name(model_name: str):
    # model 리스트로 부터 model_name이 일치하는 model을 가져와 리턴합니다
    for model in models:
        if model.name == model_name:
            return model
    raise HTTPException(status_code=404, detail=f"모델을 찾을 수 없습니다 [name: {model_name}]")

@app.post("/model", response_model=CreateModelOut)
def create_model(new_model: CreateModelIn):
    # model을 새로 만들고 model 리스트에 저장합니다
    models.append(new_model)
    return new_model

@app.patch("/model/{model_id}", response_model=UpdateModelOut)
def update_model(model_id: int, update_data: UpdateModelIn):
    # 매칭되는 model_id를 가지고 있는 모델을 업데이트합니다
    for model in models:
        if model.id == model_id:
            model = update_data
            return model
    # 매칭 되는 id를 가진 모델이 없을 때 404 에러와 메시지를 출력합니다.
    raise HTTPException(status_code=404, detail=f"모델을 찾을 수 없습니다 [id: {model_id}]")

@app.delete("/model/{model_id}")  # TODO: status code를 204로 바꿔보기
def delete_model(model_id: int):
    # TODO: 매칭되는 model_id를 가지고 있는 모델을 model 리스트로 부터 삭제합니다
    pass

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="0.0.0.0")
