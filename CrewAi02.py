
# os.environ["AGENTOPS_API_KEY"] = "2f1626b8-0696-4080-991c-553f5fb70bf5" # serper.dev API key
# AGENTOPS_API_KEY = os.getenv("2f1626b8-0696-4080-991c-553f5fb70bf5")
# import agentops
# agentops.init("29d17a90-1b65-4ebf-ac6d-fa64968f3079")

import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from openai import OpenAI
from langchain_openai import ChatOpenAI
# import agentops



# 6cd5593d7d74b7d03960308ad49561cf0432a096a379c817dc3b9bfae3285cc7
# 2f1626b8-0696-4080-991c-553f5fb70bf5
# AGENTOPS_API_KEY= "2f1626b8-0696-4080-991c-553f5fb70bf5"


os.environ["SERPER_API_KEY"] = "49031e9e1cc9a91b583771cd31a58686bdb5d645" # serper.dev API key
# os.environ["OPENAI_API_KEY"] = "Your Key"
llm=ChatOpenAI(model="Baichuan2-53B", temperature=0.7,api_key="sk-5ddfd432769737c329f61ed9442adc97",base_url="https://api.baichuan-ai.com/v1/")



# 加载工具
search_tool = SerperDevTool()

# 使用角色、目标、工具和其他属性定义您的代理
researcher = Agent(
  role='高级研究分析师',
  goal='发现人工智能和数据科学领域的前沿发展',
  backstory=(
    "您是一家领先科技智库的高级研究分析师。"
    "您擅长识别人工智能和数据科学领域的新兴趋势和技术。"
    "您善于剖析复杂数据并提供可操作的见解。"
  ),
  verbose=True,
  max_iter=15,  # Optional
  llm=llm,
  allow_delegation=False,
  # tools=[search_tool],
  max_rpm=100
)
writer = Agent(
  role='科技内容策略师',
  goal='撰写关于科技进步的引人入胜内容',
  backstory=(
    "您是一位著名的科技内容策略师，以撰写富有洞察力和引人入胜的科技和创新文章而闻名。"
    "凭借对科技行业的深刻理解，您将复杂概念转化为引人入胜的叙事。"
  ),
  verbose=True,
  max_iter=15,  # Optional
  llm=llm,
  allow_delegation=True,
  # tools=[search_tool],
  cache=False, # 为该代理禁用缓存
  max_rpm=100
)

# 为您的代理创建任务
task1 = Task(
  description=(
    "对2024年人工智能领域的最新进展进行全面分析。"
    "识别关键趋势、突破性技术和潜在的行业影响。"
    "将您的研究结果编制成详细报告。"
    "在最终确定答案之前，请确保与人类核对草稿是否合适。"
  ),
  expected_output='一份关于2024年最新人工智能进展的全面报告，不遗漏任何细节',
  agent=researcher,
  # human_input=True,
)

task2 = Task(
  description=(
    "利用研究员报告中的见解，撰写一篇引人入胜的博客文章，重点介绍最重要的人工智能进展。"
    "您的文章应既具信息性又易于理解，迎合科技爱好者的观众。"
    "力求以叙述方式捕捉这些突破性进展的本质及其对未来的影响。"
  ),
  expected_output='请用中文输出，一篇引人入胜的、格式为 markdown 的三段博客文章，介绍2024年最新人工智能进展',
  human_input=True,
  agent=writer
)


# agentops.init(AGENTOPS_API_KEY)
# 使用顺序流程实例化您的团队
crew = Crew(
  agents=[researcher, writer],
  tasks=[task1, task2],
  verbose=1,#level_map = {"debug": 1, "info": 2}
  process = Process.sequential
)

# 让您的团队开始工作！
result = crew.kickoff()
# agentops.end_session("Success")
print("#########代码执行结束#############")
# print(result)
