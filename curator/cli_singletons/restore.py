import click
from curator.cli_singletons.object_class import cli_action
from curator.cli_singletons.utils import get_width, validate_filter_json

@click.command(context_settings=get_width())
@click.option('--repository', type=str, required=True, help='Snapshot repository')
@click.option('--name', type=str, help='Snapshot name', required=False, default=None)
@click.option('--rename_pattern', type=str, help='Rename pattern', required=False, default=None)
@click.option('--rename_replacement', type=str, help='Rename replacement', required=False, default=None)
@click.option('--ignore_unavailable', is_flag=True, show_default=True, help='Ignore unavailable shards/indices.')
@click.option('--include_global_state', is_flag=True, show_default=True, help='Restore cluster global state with snapshot.')
@click.option('--partial', is_flag=True, show_default=True, help='Restore partial data (from snapshot taken with --partial).')
@click.option('--wait_for_completion/--no-wait_for_completion', default=True, show_default=True, help='Wait for the snapshot to complete')
@click.option('--skip_repo_fs_check', is_flag=True, show_default=True, help='Skip repository filesystem access validation.')
@click.option('--ignore_empty_list', is_flag=True, help='Do not raise exception if there are no actionable indices')
@click.option('--filter_list', callback=validate_filter_json, help='JSON array of filters selecting snapshots to act on.', required=True)
@click.pass_context
def restore(ctx, repository, name, rename_pattern, rename_replacement, ignore_unavailable, 
    include_global_state, partial, skip_repo_fs_check, wait_for_completion, ignore_empty_list,
    filter_list):
    """
    Restore Indices
    """
    manual_options = {
        'name': name,
        'rename_pattern': rename_pattern,
        'rename_replacement': rename_replacement,
        'ignore_unavailable': ignore_unavailable,
        'include_global_state': include_global_state,
        'partial': partial,
        'skip_repo_fs_check': skip_repo_fs_check,
        'wait_for_completion': wait_for_completion,
    }
    # ctx.info_name is the name of the function or name specified in @click.command decorator
    action = cli_action(ctx.info_name, ctx.obj['config']['client'], manual_options, filter_list, ignore_empty_list, repository=repository)
    action.do_singleton_action(dry_run=ctx.obj['dry_run'])