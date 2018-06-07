# LastPass extension for albert
Small extension for copying lastpass password to your clipboard via the albert launcher.

## Install
Clone this repo to `~/.local/share/albert/org.albert.extension.python/modules/`

## How does it work?
CLI commands:
- lp login {email}
- lp logout
- lp sync

For copying passwords just type lp and the domain you are searching the password for. All entries matching the query will be shown.
The default action copies the password to your clipboard. The alternative action copies the username.