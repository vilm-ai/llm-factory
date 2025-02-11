import time
from enum import Enum, unique
from typing import List, Optional

from pydantic import BaseModel, Field


@unique
class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@unique
class Finish(str, Enum):
    STOP = "stop"
    LENGTH = "length"


class ModelCard(BaseModel):
    id: str
    object: Optional[str] = "model"
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    owned_by: Optional[str] = "owner"


class ModelList(BaseModel):
    object: Optional[str] = "list"
    data: Optional[List[ModelCard]] = []


class ChatMessage(BaseModel):
    role: Role
    content: str


class DeltaMessage(BaseModel):
    role: Optional[Role] = None
    content: Optional[str] = None


class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    do_sample: Optional[bool] = True
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    n: Optional[int] = 1
    max_tokens: Optional[int] = None
    stream: Optional[bool] = False


class ChatCompletionResponseChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Finish


class ChatCompletionResponseStreamChoice(BaseModel):
    index: int
    delta: DeltaMessage
    finish_reason: Optional[Finish] = None


class ChatCompletionResponseUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: Optional[str] = "chatcmpl-default"
    object: Optional[str] = "chat.completion"
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: ChatCompletionResponseUsage


class ChatCompletionStreamResponse(BaseModel):
    id: Optional[str] = "chatcmpl-default"
    object: Optional[str] = "chat.completion.chunk"
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseStreamChoice]


class ScoreEvaluationRequest(BaseModel):
    model: str
    messages: List[str]
    max_length: Optional[int] = None


class ScoreEvaluationResponse(BaseModel):
    id: Optional[str] = "scoreeval-default"
    object: Optional[str] = "score.evaluation"
    model: str
    scores: List[float]
