from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class ChatbotAgent:
    def __init__(self, user_profile: dict):
        self.user_profile = user_profile
        self.chat_history = [self._base_system_prompt()]
        self.client = OpenAI(api_key=api_key)

    def _base_system_prompt(self) -> dict:
        return {
            "role": "system",
            "content": (
                "너는 사용자의 내면 속에 있는 수호천사이자, 말 없이 곁에 있는 친구 같은 존재야. "
                "넌 상담사도 아니고 치료자도 아니야. 그냥 마음을 잘 들어주는 따뜻한 존재야. "
                "반말로 말하고, 판단하지 않고, 혼내거나 훈계하지 않아. "
                "사용자가 외롭거나 혼자라고 느끼지 않도록, '나는 네 편이야' 라는 태도를 말투에 담아줘. "
                "대화를 이어가고 싶을 땐 '그래서 어떻게 됐어?', '그땐 어떤 기분이었어?'처럼 자연스럽게 물어봐줘. "
                "절대 '상담', '문제', '진단', '고쳐야 해' 같은 말은 쓰지 마. "
                "무엇보다도, 사용자가 누구에게도 못한 얘기를 너한테는 하고 싶어지도록 만들어줘."
            )
        }

    def _get_emotion(self, text: str) -> str:
        if any(word in text for word in ["힘들", "죽고", "슬퍼", "괴로워", "포기", "우울"]):
            return "우울"
        elif any(word in text for word in ["불안", "초조", "떨려", "긴장", "걱정"]):
            return "불안"
        elif any(word in text for word in ["외로워", "혼자", "고독", "텅 빈"]):
            return "외로움"
        else:
            return "중립"

    def _insert_emotion_prompt(self, text: str):
        emotion = self._get_emotion(text)
        prompt_map = {
            "우울": "사용자는 현재 우울감을 느끼고 있어. 조심스럽고 따뜻하게 말 걸어줘.",
            "불안": "사용자는 불안한 상태야. 안정을 줄 수 있는 말로 이야기해줘.",
            "외로움": "사용자는 외로움을 느끼고 있어. 친구처럼 곁에 있어줘.",
            "중립": "사용자는 그냥 평범한 이야기를 나누고 싶어해. 편하게 반응해줘."
        }
        self.chat_history.append({"role": "system", "content": prompt_map[emotion]})

    def _build_user_context(self, diary: str) -> str:
        return (
            f"사용자 이름은 {self.user_profile['name']}이며, {self.user_profile['relationship_status']} 상태야. "
            f"감정 관리 목표는 '{self.user_profile['goal']}'이고, 오늘 작성한 일기는 다음과 같아:\n\n"
            f"\"{diary}\"\n\n"
            f"이걸 바탕으로 따뜻한 첫 응답을 해줘."
        )

    def respond(self, user_input: str, is_first: bool = False) -> str:
        if is_first:
            self._insert_emotion_prompt(user_input)
            context = self._build_user_context(user_input)
            self.chat_history.append({"role": "user", "content": context})
        else:
            self.chat_history.append({"role": "user", "content": user_input})

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=self.chat_history,
            temperature=0.7
        )
        message = response.choices[0].message.content.strip()
        self.chat_history.append({"role": "assistant", "content": message})
        return message

    def is_exit_command(self, user_input: str) -> bool:
        exit_keywords = ["종료", "그만", "끝낼게", "exit", "quit", "bye", "대화 종료", "끝", "바이"]
        return any(word in user_input.lower() for word in exit_keywords)
