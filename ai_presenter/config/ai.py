from ai_presenter.config.chatgpt import ChatGPTConfig
from ai_presenter.config.defaults import TEXT_AI_FILE, VOICE_AI_FILE


class AIConfig:
    def __init__(self, data):
        try:
            self.text_ai_filename = data['text_ai_filename']
        except:
            self.text_ai_filename = TEXT_AI_FILE

        try:
            self.voice_ai_filename = data['voice_ai_filename']

        except:
            self.voice_ai_filename = VOICE_AI_FILE

        self.chatgptconfig = ChatGPTConfig(data['chatgpt_config'])
        
    def get_text_ai_filename(self) -> str:
        return self.text_ai_filename
    
    def get_voice_ai_filename(self) -> str:
        return self.voice_ai_filename
