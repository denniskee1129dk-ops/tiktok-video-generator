from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.schemas import VideoRequest, VideoResponse
from app.generator import generate_video_plan


app = FastAPI(
    title="TikTok 带货视频生成器",
    description="一个用于生成 TikTok 带货视频脚本、分镜、旁白、字幕和 Hashtags 的本地工具",
    version="1.0.0"
)


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/api/generate", response_model=VideoResponse)
def generate_video(request: VideoRequest):
    result = generate_video_plan(request)
    return result


app.mount("/static", StaticFiles(directory="static"), name="static")
