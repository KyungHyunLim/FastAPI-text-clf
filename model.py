import torch

from transformers import AutoModelForSequenceClassification, AutoTokenizer

class_dict = {
    0: 'None',
    1: 'Offensive',
    2: 'Attack',
}

def get_model(model_name:str='beomi/KcELECTRA-base')->AutoModelForSequenceClassification:
    '''모델 가져오기'''
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    return model

def get_tokenizer(model_name:str='beomi/KcELECTRA-base')->AutoTokenizer:
    '''토크나이져 가져오기'''
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    return tokenizer

def predict_from_text(
    model: AutoModelForSequenceClassification,
    tokenizer: AutoTokenizer,
    text: str)->str:
    '''text를 받아 악성 댓글 여부를 판단하여 반환'''
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=50,
        add_special_tokens=True,
    )
    pred = model(**inputs)
    classes = torch.argmax(pred['logits'].detach())
    return class_dict[classes]
    