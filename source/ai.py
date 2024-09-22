import ollama
import shutil
import asyncio
import argparse
from tqdm import tqdm
from ollama import pull



class CoreOllama :
    def __init__(self, model = "llama3.1"):
        self.model = model

        available_models = ollama.list()["models"]
        models = [model["name"].split(":")[0] for model in available_models]
        if model not in models:
            print(f"Model {model} will need to be downloaded.")
            ollama.pull(model)
        else :
            print(f"Model {model} already downloaded.")

    def multi_msg(self, messages):
        response = ollama.chat(model=self.model, messages=messages)
        print(response['message']['content'])


    def progress(self) :
        current_digest, bars = '', {}
        for progress in pull(self.model, stream=True):
          digest = progress.get('digest', '')
          if digest != current_digest and current_digest in bars:
            bars[current_digest].close()

          if not digest:
            print(progress.get('status'))
            continue

          if digest not in bars and (total := progress.get('total')):
            bars[digest] = tqdm(total=total, desc=f'pulling {digest[7:19]}', unit='B', unit_scale=True)

          if completed := progress.get('completed'):
            bars[digest].update(completed - bars[digest].n)

          current_digest = digest

    async def speak(self, speaker, content):
        if speaker:
            p = await asyncio.create_subprocess_exec(speaker, content)
            await p.communicate()

    async def chatter(self):
      parser = argparse.ArgumentParser()
      parser.add_argument('--speak', default=False, action='store_true')
      args = parser.parse_args()

      speaker = None
      if not args.speak:
        ...
      elif say := shutil.which('say'):
        speaker = say
      elif (espeak := shutil.which('espeak')) or (espeak := shutil.which('espeak-ng')):
        speaker = espeak

      client = ollama.AsyncClient()

      messages = []

      while True:
        if content_in := input('>>> '):
          messages.append({'role': 'user', 'content': content_in})

          content_out = ''
          message = {'role': 'assistant', 'content': ''}
          async for response in await client.chat(model=self.model, messages=messages, stream=True):
            if response['done']:
              messages.append(message)

            content = response['message']['content']
            print(content, end='', flush=True)

            content_out += content
            if content in ['.', '!', '?', '\n']:
              await self.speak(speaker, content_out)
              content_out = ''

            message['content'] += content

          if content_out:
            await self.speak(speaker, content_out)
          print()
