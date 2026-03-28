## Agent Memory Behavior Analysis

In this lab, I built a memory-enabled agent using Mem0 and the Strands SDK, and tested how well it can store and recall information across different sessions and users. Through the experiments with Alice and Carol, I was able to observe how the agent handles memory in a more realistic conversational setting.

In Alice’s first session, the agent was able to remember information within the same conversation. For example, after Alice mentioned that she prefers Python, the agent correctly answered a follow-up question about her programming language preference. This shows that the agent can use short-term conversational context effectively without needing to explicitly search memory every time.

More importantly, in Alice’s second session, which simulates a new session, the agent was still able to recall previously stored information. When asked what it remembered about Alice, it correctly listed her name, her role as a software engineer, her preference for Python, and the fact that she is working on a FastAPI project. This demonstrates that the agent successfully stores information in long-term memory and can retrieve it across sessions, which is the main goal of semantic memory in this system.

In contrast, the behavior in Carol’s session shows that memory is properly isolated between users. When Carol asked about her programming preferences, the agent correctly responded that it did not have that information yet. When she asked about Alice’s preferences, the agent did not reveal any information about Alice and clarified that it only has access to data from its own conversation with Carol. This indicates that the system correctly separates memory by user and avoids leaking information between users.

Another observation is how the agent handles missing information. Instead of guessing or making up an answer, the agent asks follow-up questions when it does not have enough information. This makes the interaction feel more reliable and shows that the agent can distinguish between known and unknown information.

Overall, this lab demonstrates that the agent is able to automatically store conversational information, recall it across sessions, and maintain proper separation between different users. These behaviors are important for building more realistic and production-ready AI systems that can maintain context over time without compromising user privacy.
