from pingpong.pingpong import PPManager
from pingpong.pingpong import PromptFmt

class VicunaPromptFmt(PromptFmt):
  @classmethod
  def ctx(cls, context):
    if context is None or context == "":
      return ""
    else:
      return f"""{context}

"""

  @classmethod
  def prompt(cls, pingpong, truncate_size):
    ping = pingpong.ping[:truncate_size]
    pong = "" if pingpong.pong is None else pingpong.pong[:truncate_size]
    return f"""USER: {ping}
ASSISTANT: {pong}
"""

class VicunaChatPPManager(PPManager):
  def build_prompts(self, from_idx: int=0, to_idx: int=-1, fmt: PromptFmt=VicunaPromptFmt, truncate_size: int=None):
    if to_idx == -1 or to_idx >= len(self.pingpongs):
      to_idx = len(self.pingpongs)

    results = """A chat between a curious user and an artificial intelligence assistant.
The assistant gives helpful, detailed, and polite answers to the user's questions.

"""
    results += fmt.ctx(self.ctx)

    for idx, pingpong in enumerate(self.pingpongs[from_idx:to_idx]):
      results += fmt.prompt(pingpong, truncate_size=truncate_size)

    return results