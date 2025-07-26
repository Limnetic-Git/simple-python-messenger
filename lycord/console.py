import pygame
import time

class ConsolePanel:
    def __init__(self):
        self.lines = []
        self.font = pygame.font.SysFont('consolas', 20)
        self.input_text = ""
        self.event_key = None
        self.scroll_offset = 0
        self.max_history_lines = 500  
        self.cursor_visible = True
        self.cursor_timer = 0
        
    def print_to_console(self, text: str):
        self.lines.append(f">>> {text}")
        self.scroll_to_bottom()
        
    def scroll_to_bottom(self):
        self.scroll_offset = 0
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEWHEEL:
                self.scroll_offset -= event.y 
                max_offset = max(0, len(self.lines) - self.available_lines)
                self.scroll_offset = max(0, min(self.scroll_offset, max_offset))
            elif event.type == pygame.KEYDOWN:
                self.event_key = event.unicode
                self.cursor_visible = True
                self.cursor_timer = 0
                
    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:  
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
    def blit(self, sc):
        self.write()
        WIDTH, HEIGHT = sc.get_size()
        
        self.available_height = HEIGHT - 42 - (21 + 0 * 32) - 50
        self.available_lines = self.available_height // 25
        
        y_pos = 21 + 0 * 32 - (self.scroll_offset * 25)
        max_visible_lines = self.available_lines
        
        start_idx = max(0, self.scroll_offset)
        end_idx = min(len(self.lines), start_idx + max_visible_lines)
        
        for i, line in enumerate(self.lines[start_idx:end_idx]):
            text_surface = self.font.render(line, True, 'white')
            sc.blit(text_surface, (10, 80 + i * 25))
            
        input_surface = self.font.render(f">>> {self.input_text}", True, 'green')
        sc.blit(input_surface, (10, HEIGHT - 40))

        if self.cursor_visible:
            cursor_x = 10 + self.font.size(f">>> {self.input_text}")[0]
            pygame.draw.line(sc, 'white', (cursor_x, HEIGHT - 40), 
                           (cursor_x, HEIGHT - 15), 2)
            
    def write(self):
        if self.event_key is not None:
            try:
                if ord(self.event_key) == 8:
                    self.input_text = self.input_text[:-1]
                elif ord(self.event_key) == 13:
                    pass
                elif ord(self.event_key) == 9:
                    pass
                else:
                   self.input_text += self.event_key
                self.event_key = None
            except TypeError:
                pass
