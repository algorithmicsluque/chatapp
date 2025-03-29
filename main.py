from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from datetime import datetime
import json
import os
from kivy.graphics import Color, Rectangle

# Mock data para los chats
MOCK_CHATS = [
    {
        "id": 1,
        "name": "Juan Pérez",
        "last_message": "¡Hola! ¿Cómo estás?",
        "time": "10:30",
        "unread": 2,
        "avatar": "https://i.pravatar.cc/150?img=1"
    },
    {
        "id": 2,
        "name": "María García",
        "last_message": "¿Nos vemos mañana?",
        "time": "09:15",
        "unread": 0,
        "avatar": "https://i.pravatar.cc/150?img=2"
    },
    {
        "id": 3,
        "name": "Carlos López",
        "last_message": "Perfecto, gracias",
        "time": "Ayer",
        "unread": 1,
        "avatar": "https://i.pravatar.cc/150?img=3"
    }
]

class ChatBubble(BoxLayout):
    def __init__(self, message, is_me=True, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.padding = dp(10)
        self.spacing = dp(10)
        
        if is_me:
            self.add_widget(Label(size_hint_x=0.7))
        
        bubble = BoxLayout(
            orientation='vertical',
            size_hint_x=0.7,
            padding=dp(10)
        )
        with bubble.canvas.before:
            Color(0.2, 0.6, 0.9, 1) if is_me else Color(0.8, 0.8, 0.8, 1)
            Rectangle(pos=bubble.pos, size=bubble.size)
        
        message_label = Label(
            text=message,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(40)
        )
        bubble.add_widget(message_label)
        
        if not is_me:
            self.add_widget(Label(size_hint_x=0.7))
            
        self.add_widget(bubble)

class ChatScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        header.add_widget(Label(text='Chat', font_size='20sp'))
        self.layout.add_widget(header)
        
        # Chat messages area
        self.chat_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=0.8
        )
        scroll = ScrollView()
        scroll.add_widget(self.chat_layout)
        self.layout.add_widget(scroll)
        
        # Input area
        input_area = BoxLayout(
            size_hint_y=0.1,
            padding=dp(10),
            spacing=dp(10)
        )
        self.message_input = TextInput(
            multiline=False,
            hint_text='Escribe un mensaje...',
            size_hint_x=0.8
        )
        send_button = Button(
            text='Enviar',
            size_hint_x=0.2,
            background_color=(0.2, 0.6, 0.9, 1)
        )
        send_button.bind(on_press=self.send_message)
        input_area.add_widget(self.message_input)
        input_area.add_widget(send_button)
        self.layout.add_widget(input_area)
        
        self.add_widget(self.layout)
        
        # Add some mock messages
        self.add_mock_messages()
    
    def add_mock_messages(self):
        messages = [
            ("¡Hola! ¿Cómo estás?", False),
            ("¡Hola! Muy bien, ¿y tú?", True),
            ("¿Qué planes tienes para hoy?", False),
            ("Estoy trabajando en un proyecto de Kivy", True),
            ("¡Interesante! ¿Cómo va?", False),
            ("Muy bien, estoy creando una app de chat", True)
        ]
        
        for message, is_me in messages:
            self.chat_layout.add_widget(ChatBubble(message, is_me))
    
    def send_message(self, instance):
        message = self.message_input.text.strip()
        if message:
            self.chat_layout.add_widget(ChatBubble(message, True))
            self.message_input.text = ''
            # Simulate response
            self.simulate_response()
    
    def simulate_response(self):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self.chat_layout.add_widget(
            ChatBubble("Gracias por tu mensaje, te responderé pronto.", False)
        ), 1)

class ChatsListScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        
        # Header
        header = BoxLayout(size_hint_y=0.1, padding=dp(10))
        header.add_widget(Label(text='Chats', font_size='20sp'))
        self.layout.add_widget(header)
        
        # Chats list
        scroll = ScrollView()
        self.chats_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None
        )
        self.chats_layout.bind(minimum_height=self.chats_layout.setter('height'))
        scroll.add_widget(self.chats_layout)
        self.layout.add_widget(scroll)
        
        self.add_widget(self.layout)
        self.load_chats()
    
    def load_chats(self):
        for chat in MOCK_CHATS:
            chat_item = BoxLayout(
                size_hint_y=None,
                height=dp(70),
                padding=dp(10),
                spacing=dp(10)
            )
            
            # Avatar
            avatar = Image(
                source=chat['avatar'],
                size_hint_x=0.2,
                fit_mode='cover'
            )
            chat_item.add_widget(avatar)
            
            # Chat info
            info_layout = BoxLayout(orientation='vertical', size_hint_x=0.7)
            name_label = Label(
                text=chat['name'],
                size_hint_y=0.5,
                text_size=(None, None),
                halign='left'
            )
            message_label = Label(
                text=chat['last_message'],
                size_hint_y=0.5,
                text_size=(None, None),
                halign='left'
            )
            info_layout.add_widget(name_label)
            info_layout.add_widget(message_label)
            chat_item.add_widget(info_layout)
            
            # Time and unread
            time_layout = BoxLayout(orientation='vertical', size_hint_x=0.1)
            time_label = Label(text=chat['time'])
            if chat['unread'] > 0:
                unread_box = BoxLayout(
                    size_hint=(None, None),
                    size=(dp(20), dp(20)),
                    padding=dp(2)
                )
                with unread_box.canvas.before:
                    Color(0.2, 0.6, 0.9, 1)
                    Rectangle(pos=unread_box.pos, size=unread_box.size)
                unread_label = Label(
                    text=str(chat['unread']),
                    color=(1, 1, 1, 1),
                    size_hint=(None, None),
                    size=(dp(16), dp(16))
                )
                unread_box.add_widget(unread_label)
                time_layout.add_widget(unread_box)
            time_layout.add_widget(time_label)
            chat_item.add_widget(time_layout)
            
            self.chats_layout.add_widget(chat_item)

class MainApp(App):
    def build(self):
        # Configurar el tamaño de la ventana para móvil
        Window.size = (400, 700)
        
        # Crear el gestor de pantallas
        sm = ScreenManager()
        
        # Agregar las pantallas
        sm.add_widget(ChatsListScreen(name='chats'))
        sm.add_widget(ChatScreen(name='chat'))
        
        return sm

if __name__ == '__main__':
    MainApp().run()
