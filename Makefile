old_githooks_dir := $(shell mktemp -d -t githooks-old.XXXX)

enable_flake8: pip move_old_git_hooks
	@ln -s ../githooks .git/hooks
	@git config --bool flake8.strict true
	@echo "Success! Created symlinks for .git/hooks"

move_old_git_hooks:
	@cp -r .git/hooks $(old_githooks_dir)
	@rm -rf .git/hooks
	@echo "\n\n-----------------------------------------------------------"
	@echo "Moved old git hooks to $(old_githooks_dir)"
	@echo "-----------------------------------------------------------\n\n"

pip: NaviHealth/requirements-dev.txt
	@pip install -r NaviHealth/requirements-dev.txt
