# ai-scheme.nvim

Use AI's power to creat your own neovim color scheme!

## Requirements
- `pynvim` & `neovim` (`pip install pynvim neovim`)
- `Python3`
- `Neovim (0.5.0+)`

## Installation

You can install the plugin using your favorite plugin manager. For example, using [lazy.nvim](https://github.com/folke/lazy.nvim):

```lua
local spec = {
    "yunusey/ai-scheme.nvim",
    config = function()
        require("ai-scheme").setup({--[[ your config here. See #Configuration ]]})
    end
}
```

## Configuration

The setup function accepts a table with the following keys:

```lua
M = {
	highlights = {'Function'},   -- The groups that you want highlighted.
	max_tokens = 100,            -- The maximum number of tokens to highlight (only used when `use_api` is set to true).
	use_api = false,             -- Whether to use the OpenAI API or not. If you do not want to use the API, you will be pasting the prompt to ChatGPT manually.
	use_system_clipboard = true, -- Whether to use the system clipboard or not (only used when `use_api` is set to false).
	buffer_highlight = {         -- The highlight group for the buffer that is used for prompt.
		fg = '#44ffff'
	}
}
```

## Usage

Although the plugin uses two different commands, `:PromptScheme [prompt]` & `:ChangeScheme`, however, `:ChangeScheme` is a helper command, that's why you will not need to use it.

There are two ways to use `:PromptScheme [prompt]`:
- `:PromptScheme [prompt]`
- `:PromptScheme` without the prompt which waits for the user to enter the prompt as input.

## With the API

https://github.com/yunusey/ai-scheme.nvim/assets/107340417/483b2832-ebd0-4c08-a0f5-50b3d7dee43a

When you're using the OpenAI API, the plugin will automatically use the API to generate the response which automatically highlights the highlight-groups.



## Without the API


https://github.com/yunusey/ai-scheme.nvim/assets/107340417/8fe2c923-3411-4937-a97a-e8b7acddcb83


### With the system clipboard
When you're not using OpenAI API, but using the system clipboard, the prompt that should be pasted into ChatGPT will be copied to the system clipboard. Once you get the result, you need to paste it into the window popped-up.

### Without the system clipboard
The process is almost the same as with the system clipboard. The only difference is that you need to copy the prompt to the system clipboard manually as well. Then, you need to paste it into ChatGPT. The response, then, should be pasted into the window.

## See Also
- [pynvim](https://github.com/neovim/pynvim)
- [Openai Python](https://github.com/openai/openai-python)


## Thanks
Thank you for visiting my plugin. If you liked the project and want to support, please consider giving a star, so that you can help us to reach out to more people. Thanks again!
