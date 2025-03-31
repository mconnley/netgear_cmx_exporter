ARG VARIANT=3-bookworm

FROM python:${VARIANT}

ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID



RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd --uid ${USER_UID} --gid ${USER_GID} -m ${USERNAME}


RUN apt-get update && export DEBIAN_FRONTEND=noninteractive

RUN apt-get purge -y imagemagick imagemagick-6-common \
    && python3 -m pip install --upgrade \
    pip \
    setuptools==75.6.0 \
    gitpython==3.1.41


COPY requirements.txt /tmp/pip-tmp/
COPY requirements-dev.txt /tmp/pip-tmp/

RUN pip install --no-cache-dir -r /tmp/pip-tmp/requirements.txt \
    && pip install --no-cache-dir -r /tmp/pip-tmp/requirements-dev.txt \
    && rm -rf /tmp/pip-tmp

USER ${USERNAME}