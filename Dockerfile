FROM debian:buster
MAINTAINER Seamus Tuohy (code@seamustuohy.com)

# Get Offline Release Here: https://about.draw.io/integrations/#integrations_offline
ENV RELEASE https://github.com/jgraph/drawio-desktop/releases/download/v8.8.0/draw.io-amd64-8.8.0.deb

USER root
WORKDIR /root
RUN apt-get update && apt-get install -y \
    wget \
    python3-dev \
    ca-certificates \
    make \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN wget ${RELEASE} -O draw.io.deb

RUN apt-get update \
    && dpkg -i draw.io.deb || true \
    && apt install -f -y \
    && apt install -y \
    libx11-xcb1 \
    libasound2 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# --install-suggests

# python3-dev \
# gconf-service \
# gconf2 \
# gconf2-common \
# libappindicator1 \
# libdbus-glib-1-2 \
# libdbusmenu-glib4 \
# libdbusmenu-gtk4 \
# libgail-common \
# libgail18 \
# libgconf-2-4 \
# libgtk2.0-0 \
# libgtk2.0-bin \
# libgtk2.0-common \
# libindicator7 \
# libnotify4 \
# libpython-stdlib \
# libpython2-stdlib \
# libpython2.7-minimal \
# libpython2.7-stdlib \
# libxss1 \
# libxtst6 \
# notification-daemon \
# psmisc \
# python \
# python-minimal \
# python2 \
# python2-minimal \
# python2.7 \
# python2.7-minimal \
# x11-common

# # Create Unprivlaged User
# RUN groupadd -r user && \
#   useradd -r -g user -d /home/user -s /sbin/nologin -c "User" user && \
#   mkdir /home/user && \
#   chown -R user:user /home/user

USER root
WORKDIR /root
CMD ["draw.io"]
