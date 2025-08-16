# examples/hooks/logging_hooks.py

import os
from agents import Agent, Runner  # SDK public imports
from agents import AgentHooks  # lifecycle hooks

# Minimal hooks: log start/end/error without any globals at import time
class LoggingHooks(AgentHooks[dict]):
    async def on_start(self, context, agent):
        # context.input may be string or structured input
        print(f"[HOOK on_start] agent={agent.name!r} input={getattr(context, 'input', None)!r}")

    async def on_end(self, context, agent, output):
        # output may be text or structured; show the final_output if available
        try:
            final_text = getattr(output, "final_output", output)
        except Exception:
            final_text = output
        print(f"[HOOK on_end] agent={agent.name!r} output={final_text!r}")

    async def on_error(self, context, agent, error: Exception):
        print(f"[HOOK on_error] agent={agent.name!r} error={error!r}")

def main():
    # Create a simple agent
    agent = Agent(
        name="Hooked Assistant",
        instructions="You are a concise assistant.",
    )

    # Attach hooks (no global singletons)
    agent.hooks = LoggingHooks()

    # Get input and run
    user_input = "Give me one fun fact about space."
    result = Runner.run_sync(agent, user_input)

    # Print final output for the example
    print("\n=== FINAL OUTPUT ===")
    print(result.final_output)

if __name__ == "__main__":
    # Make sure the API key is set before running:
    #   set OPENAI_API_KEY=sk-...   (Windows)
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Please set OPENAI_API_KEY before running this example.")
    main()
