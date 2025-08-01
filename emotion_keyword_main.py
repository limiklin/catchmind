from emotion_keyword_agent import EmotionKeywordAgent

# 일기 예시
diary = "오늘 나는 여자친구랑 싸웠어. 내가 여자친구의 돈까스를 말 없이 빼앗어 먹었거든. 그래서 여자친구에게 햄버거를 사줬어. 여자친구는 바보야."

agent = EmotionKeywordAgent()
result = agent.run(diary)

print("🎯 감정:", result["emotion"])
print("🔑 키워드:", result["keywords"])
