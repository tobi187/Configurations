alias cgit="/home/tobi/projects/services/cgit/main.py"
alias l="ls"
alias ll="ls -al"
alias c="clear"
alias ccat='pygmentize -g'
alias tldr='python3 -m tldr'
alias py='python3'
alias va='source ./.venv/bin/activate'

eval $(keychain --eval id_rsa --noask)

function mcd() {
    mkdir -p "$1"
    cd "$1"
}
