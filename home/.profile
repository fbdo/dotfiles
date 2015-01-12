# ~/.profile: executed by the command interpreter for login shells.
# This file is not read by bash(1), if ~/.bash_profile or ~/.bash_login
# exists.
# see /usr/share/doc/bash/examples/startup-files for examples.
# the files are located in the bash-doc package.

# the default umask is set in /etc/profile; for setting the umask
# for ssh logins, install and configure the libpam-umask package.
#umask 022

# if running bash
if [ -n "$BASH_VERSION" ]; then
    # include .bashrc if it exists
    if [ -f "$HOME/.bashrc" ]; then
	. "$HOME/.bashrc"
    fi
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

JAVA_HOME=/usr/lib/jvm/java-7-oracle
M2_HOME="/opt/maven"
M2="$M2_HOME/bin"
APPENGINE_HOME="/home/fabio/Applications/appengine-java-sdk"
GRADLE_HOME="/home/fabio/Applications/gradle" 
PATH="$HOME/Applications/activator:/opt/scala/bin:$M2:$APPENGINE_HOME/bin:$GRADLE_HOME/bin:$PATH"
ANSIBLE_HOSTS=/home/fabio/Applications/ansible/ansible_hosts
