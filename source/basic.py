import ollama

from ai import CoreOllama

class BasicLLM(CoreOllama):
    def __init__(self, model):
        super().__init__(model)

    def test_run(self) :
        response = ollama.chat(model=self.model, messages=[
          {
            'role': 'user',
            'content': 'Why is the sky blue?',
          },
        ])
        print(response['message']['content'])
