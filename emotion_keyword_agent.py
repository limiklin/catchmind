from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class EmotionKeywordAgent:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)
        self.emotion_map = {
            "기쁨": "joy",
            "슬픔": "sadness",
            "화남": "anger",
            "중립": "neutral"
        }

    def run(self, diary_text: str) -> dict:
        system_prompt = """
당신은 감정 분석과 키워드 추출 전문가입니다.

[목표]
- 사용자의 일기 내용을 분석하여 감정을 1개 추출하세요.
- 감정은 반드시 다음 중 하나여야 합니다: 기쁨, 슬픔, 화남, 중립
- 일기에서 핵심 키워드 3~5개를 한국어로 추출한 후, 영어로 번역해서 같이 제공하세요.

[응답 형식 예시]
{
  "emotion": "슬픔",
  "keywords_ko": ["학교", "혼자", "비"],
  "keywords_en": ["school", "alone", "rain"]
}
반드시 위 JSON 형식만 출력하세요.
"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"일기: {diary_text}"}
            ],
            temperature=0.4
        )

        raw = response.choices[0].message.content

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            raise ValueError(f"GPT 응답이 JSON이 아닙니다: {raw}")

        # 감정 한국어 → 영어 매핑
        emotion_kr = parsed["emotion"]
        emotion_en = self.emotion_map.get(emotion_kr)
        if not emotion_en:
            raise ValueError(f"감정 '{emotion_kr}'은 허용되지 않은 값입니다.")

        return {
            "emotion": emotion_en,
            "keywords": parsed["keywords_en"]
        }
