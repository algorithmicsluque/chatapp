from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import (
    StringProperty, 
    ListProperty, 
    ObjectProperty, 
    BooleanProperty,
    NumericProperty
)
from kivy.lang import Builder
from kivy.resources import resource_find
from kivy.animation import Animation
import json
from datetime import datetime


class ChatScreen(BoxLayout):
    current_chat_title = StringProperty('Select a chat')
    chats = ListProperty([])
    current_chat = ObjectProperty(None)
    nav_width = NumericProperty(0.25)
    is_nav_open = BooleanProperty(True)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_chats()
        if not self.chats:
            self.create_new_chat(initial=True)
    
    def toggle_nav(self):
        target_width = 0.25 if not self.is_nav_open else 0.0
        anim = Animation(nav_width=target_width, duration=0.3)
        anim.start(self)
        self.is_nav_open = not self.is_nav_open
    
    def load_chats(self):
        try:
            with open('data.json', 'r') as f:
                self.chats = json.load(f).get('chats', [])
                self.update_chat_list()
        except (FileNotFoundError, json.JSONDecodeError):
            self.chats = []
    
    def save_chats(self):
        with open('data.json', 'w') as f:
            json.dump({'chats': self.chats}, f, indent=4)
    
    def update_chat_list(self):
        self.ids.chat_list.data = [
            {'text': chat['title'], 'on_press': lambda x=chat: self.select_chat(x)} 
            for chat in self.chats
        ]
    
    def create_new_chat(self, initial=False):
        new_chat = {
            'id': len(self.chats) + 1,
            'title': f'Chat {len(self.chats) + 1}',
            'timestamp': datetime.now().isoformat(),
            'messages': []
        }
        self.chats.append(new_chat)
        self.update_chat_list()
        if not initial:
            self.select_chat(new_chat)
        self.save_chats()
    
    def select_chat(self, chat):
        self.current_chat = chat
        self.current_chat_title = chat['title']
        self.update_messages()
    
    def update_messages(self):
        self.ids.chat_messages.data = [
            {'text': msg['content'], 'is_user': msg['role'] == 'user'} 
            for msg in self.current_chat['messages']
        ]
        self.ids.chat_scroll.scroll_y = 0
    
    def on_message_submit(self, instance):
        self.send_message()
        return True
    
    def send_message(self):
        message = self.ids.message_input.text.strip()
        if not message or not self.current_chat:
            return
        
        user_msg = {
            'content': message,
            'role': 'user',
            'timestamp': datetime.now().isoformat()
        }
        
        bot_msg = {
            'content': 'This is a simulated response.',
            'role': 'assistant',
            'timestamp': datetime.now().isoformat()
        }
        
        self.current_chat['messages'].extend([user_msg, bot_msg])
        self.ids.message_input.text = ''
        self.update_messages()
        self.save_chats()
    
    def clear_chats(self):
        self.chats = []
        self.current_chat = None
        self.current_chat_title = 'Select a chat'
        self.update_chat_list()
        self.ids.chat_messages.data = []
        self.save_chats()

class ChatApp(App):
    def build(self):
        Window.clearcolor = (1, 1, 1, 1)  # Fondo blanco
        return ChatScreen()

if __name__ == '__main__':
    from kivy.core.window import Window
    ChatApp().run()