from basic import BasicLLM
import asyncio
import threading

messages_test = [{
  'role': 'user',
  'content': 'if a tree falls in the forest and no one is around to hear it, does it make a sound?',
},
{
  'role': 'user',
  'content': 'Why is the sky blue?',
}]

json_test = [{
    'role' : 'user',
    'content' : 'create a json object with a key of "name"\
    and a value of "ollama" and only respond with json object'
}]

def chat(chatter) :
    try:
      asyncio.run(chatter())
    except (KeyboardInterrupt, EOFError):
        print()
        print('Goodbye!')
        print()

if __name__ == '__main__':
    model = BasicLLM(model="mistral")
    threads = [
    # threading.Thread(target=model.test_run, args=()),
    # threading.Thread(target=model.progress, args=()),
    # threading.Thread(target=chat, args=(model.chatter,)),
    threading.Thread(target=model.multi_msg, args=(json_test,)),
    ]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    #
