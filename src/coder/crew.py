from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai import LLM
import os
from dotenv import load_dotenv
load_dotenv()

llm = LLM(
    model="gemini-3.5-flash-lite",
    base_url="https://api.mixroute.ai/v1",
    api_key=os.getenv("MIXROUTE_API_KEY")
)

llm1 = LLM(
    model="deepseek-v4-flash",
    base_url="https://api.mixroute.ai/v1",
    api_key=os.getenv("MIXROUTE_API_KEY")
)

@CrewBase
class Coder():
    """Coder crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def coder(self) -> Agent:
        return Agent(
            llm=llm,
            config=self.agents_config['coder'],
            allow_code_execution=True,
            code_execution_mode="safe",
            max_execution_time=30,
            max_retry_limit=5,
            verbose=True
        )



    @task
    def coding_task(self) -> Task:
        return Task(
            config=self.tasks_config['coding_task'],
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Coder crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
