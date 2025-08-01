from chatbot_agent import ChatbotAgent

user_profile = {
    "name": "현성",
    "nickname": "이믹인",
    "relationship_status": "여자친구와 1년째 연애 중",
    "birthday": "9월 15일",
    "goal": "감정 기록을 통해 나 자신을 더 잘 이해하고 싶음"
}

agent = ChatbotAgent(user_profile)

diary_text = input("📝 오늘의 일기를 입력해주세요:\n")

response = agent.respond(diary_text, is_first=True)
print("🤖:", response)

while True:
    try:
        user_input = input("🙂: ")
        if agent.is_exit_command(user_input):
            print("🤖: 오늘 이야기해줘서 고마워. 언제든 또 와!")
            break
        reply = agent.respond(user_input)
        print("🤖:", reply)
    except KeyboardInterrupt:
        print("\n🤖: 괜찮아, 다음에 또 얘기하자 :)")
        break
