import json
import logging
import os
from typing import (
    Any,
    Generator,
)

from awscli.autocomplete.main import (  # type: ignore[import-untyped]
    create_autocompleter,
)
from awscli.autoprompt.prompttoolkit import (  # type: ignore[import-untyped]
    Completer,
    PromptToolkitCompleter,
    ThreadedCompleter,
)
from awscli.clidriver import create_clidriver  # type: ignore[import-untyped]
from prompt_toolkit.completion.base import (
    CompleteEvent,
)
from prompt_toolkit.document import Document

LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_completions(
    completer: Completer, doc: Document, event: CompleteEvent
) -> Generator[dict[str, Any], None, None]:
    results = completer.get_completions(doc, event)

    for result in results:
        comp_result = {
            "text": result.text,
            "start_position": result.start_position,
            "display_text": result.display_text,
            "display_meta": result.display_meta_text,
        }

        if LOGGER.isEnabledFor(logging.DEBUG):
            logging.debug(f"result: {comp_result}")

        yield comp_result


def main() -> None:
    cli_driver = create_clidriver()
    completer = ThreadedCompleter(
        PromptToolkitCompleter(create_autocompleter(driver=cli_driver))
    )

    # bash exports COMP_LINE and COMP_POINT, tcsh COMMAND_LINE only
    command_line = os.environ.get("COMP_LINE") or os.environ.get("COMMAND_LINE") or ""
    command_index = int(os.environ.get("COMP_POINT") or len(command_line))

    # the completer expects `aws` to be omitted
    if command_line.startswith("aws "):
        command_line = command_line[4:]
        command_index = max(0, command_index - 4)

    doc = Document(command_line, command_index)
    event = CompleteEvent(completion_requested=True)

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"command_line: {command_line}")

    try:
        for comp in get_completions(completer, doc, event):
            print(json.dumps(comp))
    except KeyboardInterrupt:
        # If the user hits Ctrl+C, we don't want to print
        # a traceback to the user.
        return


if __name__ == "__main__":
    main()
