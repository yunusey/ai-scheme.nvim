local M = {}

M = {
	highlights = {
		'Function',
		'Variable',
		'Keyword',
		'Constant',
		'String',
		'Comment',
		'Number',
		'Boolean',
		'Float',
		'Identifier',
		'Operator',
		'PreProc',
		'Include',
		'Define',
		'Macro',
	},
	max_tokens = 100,
	use_api = false,
	use_system_clipboard = true,
	buffer_highlight = {
		fg = '#44ffff'
	}
}

M.setup = function(settings)
	for k, v in pairs(settings) do
		M[k] = v
	end
end

return M
