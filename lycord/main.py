import pygame, socket, time
import sys
from console import ConsolePanel

ClientSocket = socket.socket()
host = '127.0.0.2'
port = 1234
print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))
    
client_id = ClientSocket.recv(20480).decode('utf-8')
ClientSocket.send(str.encode(f'Anonimous_{client_id}'))

pygame.init()

WIDTH, HEIGHT = 800, 600
sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

console_panel = ConsolePanel()  
clock = pygame.time.Clock()
running = True
current_message = None
messages_in_chat = []
def main():
    global running, current_message, messages_in_chat
    messages_in_chat = eval(ClientSocket.recv(20480).decode('utf-8'))
    for message in messages_in_chat:
        console_panel.lines.append(f'{message["author"]}: {message["text"]}')
    while running:
        dt = clock.tick(60) / 1000.0
        events = pygame.event.get()
                
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_RETURN:
                    if console_panel.input_text != "":
                        #console_panel.print_to_console(console_panel.input_text)
                        curr_time = time.strftime("%H:%M:%S", time.localtime())
                        current_message = {'text': console_panel.input_text, 'author': f'Anonimous_{client_id}', 'time': curr_time}
                        console_panel.input_text = ""
                        
        pack = current_message
        ClientSocket.send(str.encode(str(pack)))
        new_messages = eval(ClientSocket.recv(20480).decode('utf-8'))
        for message in new_messages:
            finded = False
            for old_message in messages_in_chat:
                if message['id'] == old_message['id']:
                    finded = True
                    break
            if not finded:
                looks_to_last_line = (console_panel.scroll_offset == max(0, len(console_panel.lines) - console_panel.available_lines))
                console_panel.lines.append(f'{message["author"]}: {message["text"]}')
                messages_in_chat.append(message)
                if looks_to_last_line:
                    console_panel.scroll_offset = max(0, len(console_panel.lines) - console_panel.available_lines)

                        
        console_panel.handle_events(events)
        console_panel.update(dt)

        sc.fill(BLACK)
        
        console_panel.blit(sc)
        
        pygame.display.update()
        current_message = None
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()