from typing import List
from pydantic import BaseModel, Field


class VideoRequest(BaseModel):
    product_name: str = Field(..., description="产品名称")
    target_audience: str = Field(..., description="目标用户")
    selling_points: str = Field(..., description="核心卖点")
    price: str = Field(..., description="产品价格")
    style: str = Field(..., description="视频风格")
    duration: int = Field(default=30, description="视频时长")
    language: str = Field(default="中文", description="输出语言")
    template_type: str = Field(default="痛点带货", description="脚本模板类型")


class StoryboardItem(BaseModel):
    time: str
    scene: str
    visual: str
    voiceover: str
    subtitle: str
    ai_prompt: str


class VideoResponse(BaseModel):
    title: str
    hook: str
    script_summary: str
    template_type: str
    storyboard: List[StoryboardItem]
    caption: str
    hashtags: List[str]
    tips: List[str]
