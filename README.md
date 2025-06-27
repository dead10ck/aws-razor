# `aws-razor`

*At last, my arm is complete again!*

This tool is an alternative to awscli's built-in completion prompt. This tool
uses the same auto completion machinery from the CLI's code, but simply writes
the completion results as plain JSON objects (one per line) so that it can be
used for any completion frontend, such as bash, fish, or nushell.
