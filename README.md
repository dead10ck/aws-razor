# `aws-razor`

*At last, my arm is complete again!*

This tool is an alternative to awscli's built-in completion prompt. It uses
the same auto completion machinery from the CLI's code, but simply writes the
completion results as plain JSON objects, one per line. It is primarily intended
for completion frontends that accept more context than just the completion text,
such as descriptions, e.g. nushell; although, it can be used for any completion
frontend.

## Usage

For Nushell,

```nushell
def "nu-complete aws" [context: string, pos: int] {
  aws-razor --command-line $context --position $pos
  | from json --objects
  | each {|completion|
    {
      value: $completion.text,
      description: $completion.display_meta,
    }
  }
}

export extern "aws" [
  ...command: string@"nu-complete aws"
]
```

## Installation

Note this requires `awscli` v2, which is not available on PyPI. This tool can
be installed to either the system so that it uses the system's python path, or
installed in a virtualenv together with the awscli from git. In the virtualenv,
you can install awscli from the `v2` branch of the git repo along with this
tool, e.g.

```
uv tool install aws-razor --with "git+https://github.com/aws/aws-cli.git@v2"
```
