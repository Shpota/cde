#!/usr/bin/env python3
from subprocess import Popen, check_output, call


def create_app():
    branch = current_branch()
    run('docker build . -t cde:' + branch)
    run('docker tag cde:' + branch
        + ' localhost:5000/cde:' + branch)
    run('docker push localhost:5000/cde:' + branch)
    create_resources(branch)


def create_resources(branch: str):
    content = file_content('k8s/resources.yml') \
        .replace('{{ NAME }}', branch)
    call('echo "%s" | microk8s.kubectl apply -f -'
         % content, shell=True)


def current_branch() -> str:
    return check_output([
        'git', 'rev-parse', '--abbrev-ref', 'HEAD'
    ]).decode('utf-8').replace('\n', '')


def file_content(filename: str) -> str:
    with open(filename, 'r') as file:
        return file.read()


def run(command: str):
    Popen(command.split(' ')).wait()


if __name__ == '__main__':
    create_app()
