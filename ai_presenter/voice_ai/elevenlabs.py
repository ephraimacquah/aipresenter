from ai_presenter.voice_ai.base import VoiceAI, VoiceAIActor
from ai_presenter.database import Database
from ai_presenter.config.voice import VoiceConfig
from elevenlabs import generate, save, Iterator, VoiceDesign, Voice
import logging


class VoiceAIActorElevenLabs(VoiceAIActor):
    def __init__(self, config: VoiceConfig):
        super().__init__(config)

        self.sample_text = f'I am {self.name}. I am a {self.age} year old ' + \
            f'{self.gender} with a {self.accent} accent.' + \
            f'I am {self.name}. I am a {self.age} year old ' + \
            f'{self.gender} with a {self.accent} accent.'

        logging.info(f"designing a voice for {self.name}")
        self.voice_design = VoiceDesign(name=self.name,
                                        text=self.sample_text,
                                        gender=self.gender,
                                        age=self.age, accent=self.accent,
                                        accent_strength=self.accent_strength)

        self.voice = Voice.from_design(self.voice_design)

    # .says takes the message and generates audio from that message
    # note: for the real voiceaiactor class, the elevenlabs generate
    # methods return raw data called audio which can be manipulated before
    # saving to a file(ie. concatenation)
    def says(self, message, emotion) -> (bytes | Iterator[bytes]):
        logging.info(f'{self.name} says {message} in a {emotion} way')
        audio = generate(text=message, model="eleven_monolingual_v1",
                         voice=self.voice)
        return audio


class ElevenLabs(VoiceAI):
    def __init__(self, db: Database):
        super().__init__(db)

    def new_actor(self, config):
        return VoiceAIActorElevenLabs(config)

    # make narrator actor
    # open file and create a new actor for each character
    # for each line of dialogue, input it into actor.says
    # actor.says returns audio output
    # this is concatenated with previous actor.says outputs
    # output file opened and audio output is written to output_file
    # this is saved into output file
    # return output file

    def generate(self, input_file: str, output_file: str):
        logging.info('ElevenLabs: Generating audio file')
        # need suggestions as to format of json
        # as well as parsing it
        audio = bytes()
        with open(input_file, 'r') as file:
            for line in file:
                # load characters in character db
                data = self.create_character_db(line)

                # now go through dialogue and create audio
                for message in data['dialogue']:
                    name = message['speaker']
                    text = message['message']
                    emotion = message['emotion']
                    logging.info('ElevenLabs: Stitching together audio')
                    audio += self.characters[name].says(text, emotion)
        logging.info(f"ElevenLabs: Audio can be found in {output_file}")
        save(audio, output_file)
