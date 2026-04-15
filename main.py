import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

# 1. تحميل المفتاح السري بتاعك
load_dotenv()

# 2. توصيل العقل (بالطريقة الجديدة لـ CrewAI 1.x)
groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# 3. خلق الموظف الأول (The Analyst)
analyst = Agent(
    role='Senior Deal Intelligence Analyst',
    goal='Analyze B2B suppliers and find the most cost-effective and secure deals.',
    backstory='You are a ruthless and brilliant business analyst working for a top corporate firm. You only care about data, ROI, and proving mathematically why a deal is the best choice.',
    verbose=True,
    allow_delegation=False,
    llm=groq_llm
)

# 4. تحديد المهمة (The Task - Scenario)
negotiation_task = Task(
    description='''
    Compare these two cloud infrastructure suppliers for our company:
    - Supplier A: Costs $50,000/year, 99.9% uptime, standard email support.
    - Supplier B: Costs $65,000/year, 99.99% uptime, premium 24/7 dedicated support team.
    
    Our company loses roughly $5,000 for every hour of downtime. 
    
    Write a short, punchy decision on which supplier to choose. PROVE why it's the right business decision using the downtime financial loss as the core argument.
    ''',
    expected_output='A definitive recommendation choosing Supplier A or B, including the mathematical justification and ROI calculation.',
    agent=analyst
)

# 5. تشغيل النظام (The Crew)
deal_crew = Crew(
    agents=[analyst],
    tasks=[negotiation_task],
    verbose=True,
    process=Process.sequential
)

print("🚀 Booting up the Autonomous Deal AI...\n")
result = deal_crew.kickoff()

print("\n==============================================")
print("🔥 THE AI'S FINAL DECISION 🔥")
print("==============================================")
print(result)
