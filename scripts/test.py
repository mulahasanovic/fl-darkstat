import click
from .universal import say, PROJECT_CORE


@click.group()
def test():
    "testing commands"
    pass


@test.command()
def pylint():
    "link with pylint"
    say("pylint --load-plugins pylint_django --django-settings-module="
        '"' + f"{PROJECT_CORE}" + '.settings"'
        " --disable=django-not-configured `ls -d */`"
        )


@test.command()
def flake():
    "lint with flake8"
    say("flake8 --exclude .git,venv,migrations .")


@test.command()
def unit():
    "get unit tests"
    say("coverage run --omit 'venv/*' --source='.' manage.py test")


@test.command()
def cover():
    """get coverage of unit tests
    it should be used only after 'unit' command"""
    say("coverage report")
