import pynvim
import re
import openai
import os

LOG_FILE = './log.txt'

OPENAI_PROMPT = (
    "Assign colors to each of these highlight groups "
    "that are related to the user prompt:\n"
    "You should know that they will be used to highlight Neovim text.\n"
    "So that, you should not have very similar colors one next another.\n"
    "For instance, function and class should not be in the same color, "
    "because they can be next to each other\n"
    "User's prompt: {}\n"
    "Highlight groups: {}\n"
    "Keep in mind that they will be put on a dark background.\n"
    "All the colors should be seen by the user easily.\n"
    "Only give me the output and nothing else.\n"
    "They will be in this format:\n"
    "{{highlight_group_name}}: #rrggbb\n"
    "Example: \n"
    "Function: #ff0312\n"
)


@pynvim.plugin
class AiScheme(object):
    def __init__(self, nvim: pynvim.Nvim):
        self.nvim = nvim

        self.highlights = self.nvim.call('luaeval',
                                         'require("ai-scheme").highlights')
        self.buffer_highlight = \
            self.nvim.call('luaeval',
                           'require("ai-scheme").buffer_highlight')
        self.use_api = self.nvim.call('luaeval',
                                      'require("ai-scheme").use_api')
        self.max_tokens = self.nvim.call('luaeval',
                                         'require("ai-scheme").max_tokens')
        self.use_system_clipboard = \
            self.nvim.call('luaeval',
                           'require("ai-scheme").use_system_clipboard')

        self.elements = (None, None)
        self.nvim.api.set_hl(0, 'AIScheme', self.buffer_highlight)

    @pynvim.command("ChangeScheme", range='', nargs='*')
    def change_scheme(self, args: list, range):
        buf, win = self.elements
        if buf is None or win is None or self.use_api:
            return

        contents = self.nvim.api.buf_get_lines(buf.number, 0, -1, False)

        self.nvim.api.win_close(0, True)  # I did not manage to use `win`py
        self.nvim.api.buf_delete(buf.number, {'force': True})

        answer = []

        for line in contents[::-1]:
            if line != "# Paste the answer here: ":
                answer.append(line)
            else:
                break

        answer.reverse()

        pattern = r'(.*?): (#[0-9a-fA-F]{6})'
        for var, fg in re.findall(pattern, '\n'.join(answer)):
            self.nvim.api.set_hl(0, var, {'fg': fg})

    @pynvim.command("PromptScheme", range='', nargs='*')
    def prompt_scheme(self, args: list, range):
        prompt = ' '.join(args)

        if prompt.isspace() or prompt == '':
            prompt = self.nvim.funcs.input('Please enter your prompt: ')

        self.get_prompt(prompt)

    def show_prompt(self, quest: str):
        buf = self.nvim.api.create_buf(False, True)

        win = self.nvim.api.open_win(buf, False, {
            'relative': 'editor',
            'style': 'minimal',
            'row': 10,
            'col': 10,
            'width': 70,
            'height': 8,
            'border': 'rounded',
        })

        self.nvim.api.buf_set_name(buf, '')
        self.nvim.api.buf_set_option(buf, 'modifiable', True)
        self.nvim.api.buf_set_lines(buf, 0, -1, True, quest.split('\n'))
        self.nvim.api.buf_set_keymap(buf, 'n', '<CR>', ':ChangeScheme<CR>', {
            'noremap': True
        })

        for linenr in range(len(buf)):
            buf.add_highlight('Comment', linenr, 0, 1)
            buf.add_highlight('AIScheme', linenr, 1, -1)

        self.nvim.api.set_current_win(win)
        win = self.nvim.api.get_current_win()
        self.nvim.command('normal Go')  # Go to the end and enter a new line

        self.elements = (buf, win)

    def get_prompt(self, prompt: str):
        highlights = self.nvim.api.get_hl(0, {})

        self.give_prompt(prompt, highlights.keys())

    def give_prompt(self, prompt: str, keys: list) -> str:

        file = open(LOG_FILE, 'w')
        prompt_given = OPENAI_PROMPT.format(prompt, self.highlights)
        file.write(prompt_given)
        file.close()

        if self.use_api:
            openai.api_key = os.getenv('OPENAI_API_KEY')
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt_given,
                max_tokens=self.max_tokens,
            ).choices[0].text

            pattern = r'(.*?): (#[0-9a-fA-F]{6})'
            for var, fg in re.findall(pattern, response):
                self.nvim.api.set_hl(0, var, {'fg': fg})
        else:
            a = (
                "# Prompt: {}\n"
                "Paste the answer here: "
            )

            if self.use_system_clipboard:
                self.nvim.call('setreg', '+', prompt_given)
                self.nvim.out_write('Copied to clipboard!\n')

            self.show_prompt(a.format(prompt_given).replace('\n', '\n# '))
