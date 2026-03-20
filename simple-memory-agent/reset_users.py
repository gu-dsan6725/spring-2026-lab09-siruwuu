from agent import Agent

for user in ["alice", "carol"]:
    a = Agent(user_id=user, run_id="reset-run")
    a.reset_memory()
    print(f"Reset memory for {user}")