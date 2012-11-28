import os
import sublime
import sublime_plugin
import ci_ide_helper


class GenerateCodeintelHelperCommand(sublime_plugin.WindowCommand):
    def run(self):
        # get base ide helper
        print 'start plugin'

        # content = open('ci_ide_helper.php').read()
        content = ci_ide_helper.contents

        # get root folder
        top_folders = self.window.folders()
        for top_folder in top_folders:
            top_folder_contents = os.listdir(top_folder)
            if 'index.php' in top_folder_contents:
                self.root = top_folder
                break

            else:
                for secondary_folder in top_folder_contents:
                    dir = top_folder + '/' + secondary_folder + '/'

                    if os.path.isdir(dir):
                        dir_contents = os.listdir(dir)
                        if 'index.php' in dir_contents:
                            self.root = dir
                            break
        if not hasattr(self, 'root'):
            sublime.status_message('Could not find project root')
            return

        # get model names
        model_dirs = [x[0] for x in os.walk(os.path.join(self.root, 'application')) if 'models' in x[0]]
        models = []
        for model_dir in model_dirs:
            files = os.listdir(model_dir)
            for f in files:
                if f[-4:] == '.php':
                    models.append(f[:-4])

        # add in user models
        rep = ' * ==============START USER DEFINED MODELS===============\n */\nc'
        content = content.replace(' */\nc', rep)

        settings = sublime.load_settings('CI Codeintel Helper.sublime-settings')
        strip_model = settings.get('strip_model')
        for model in models:
            model_class = ''.join([model[0].upper(), model[1:]])
            if strip_model:
                model_var = model.replace('_model', '')
            else:
                model_var = model

            rep = ' * @property %s $%s    User Defined model\n */\nc' % (model_class, model_var)
            content = content.replace(' */\nc', rep)

        print contents
        # write helper file
        with open(os.path.join(self.root, 'ci_ide_helper.php'), 'w') as f:
            f.write(content)
