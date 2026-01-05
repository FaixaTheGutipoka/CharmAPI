from pydantic import BaseModel
from typing import Literal

Context = Literal["classic", "nerdy"]
Tone = Literal["funny", "casual", "professional"]

class FlirtResponse(BaseModel):
    flirt: str
    context: str
    tone: str
    source: str
