from django.core.management.base import NoArgsCommand
from mediagenerator.api import generate_media

class Command(NoArgsCommand):
    help = 'Combines and compresses your media files and saves them in _generated_media.'

    requires_model_validation = False

    def handle_noargs(self, **options):
        generate_media()
