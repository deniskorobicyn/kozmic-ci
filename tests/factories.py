import hashlib
import datetime

import factory.alchemy

from kozmic.models import (db, User, Project, Membership, Hook, TrackedFile,
                           HookCall, Build, Job, Organization)


class Factory(factory.alchemy.SQLAlchemyModelFactory):
    FACTORY_SESSION = None
    ABSTRACT_FACTORY = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        obj = super(Factory, cls)._create(target_class, *args, **kwargs)
        cls.FACTORY_SESSION.commit()
        return obj


def setup(session):
    Factory.FACTORY_SESSION = session


def reset():
    factories = (
        UserFactory,
        ProjectFactory,
        MembershipFactory,
        UserRepositoryFactory,
        OrganizationFactory,
        OrganizationRepositoryFactory,
        BuildFactory,
        JobFactory,
        HookFactory,
        TrackedFileFactory,
        HookCallFactory,
    )
    for factory in factories:
        factory.reset_sequence()


_identity = lambda n: n


class UserFactory(Factory):
    FACTORY_FOR = User

    id = factory.Sequence(_identity)
    gh_id = factory.Sequence(_identity)
    gh_name = factory.Sequence(u'User {}'.format)
    gh_login = factory.Sequence(u'user_{}'.format)
    gh_avatar_url = factory.Sequence(u'http://example.com/{}.png'.format)
    gh_access_token = 'token'


class UserRepositoryFactory(Factory):
    FACTORY_FOR = User.Repository

    id = factory.Sequence(_identity)
    gh_id = factory.Sequence(lambda n: 1000 + n)
    gh_name = 'django'
    gh_full_name = 'johndoe/django'

    @factory.lazy_attribute
    def gh_clone_url(self):
        return 'git://github.com/{}.git'.format(self.gh_full_name)


class OrganizationFactory(Factory):
    FACTORY_FOR = Organization

    id = factory.Sequence(_identity)
    gh_id = factory.Sequence(_identity)
    gh_login = 'pyconru'
    gh_name = 'PyCon Russia'


class OrganizationRepositoryFactory(Factory):
    FACTORY_FOR = Organization.Repository

    id = factory.Sequence(lambda n: n)
    gh_id = factory.Sequence(lambda n: 2000 + n)
    gh_name = 'django'
    gh_full_name = 'johndoe/django'

    @factory.lazy_attribute
    def gh_clone_url(self):
        return 'git://github.com/{}.git'.format(self.gh_full_name)


class MembershipFactory(Factory):
    FACTORY_FOR = Membership


class ProjectFactory(Factory):
    FACTORY_FOR = Project

    id = factory.Sequence(_identity)
    gh_id = factory.Sequence(_identity)
    gh_name = factory.Sequence(u'project_{}'.format)
    gh_full_name = factory.Sequence(u'project_{0}/project_{0}'.format)
    gh_login = factory.Sequence(u'project_{}'.format)
    gh_clone_url = factory.Sequence(u'git://example.com/%d.git'.format)
    gh_key_id = factory.Sequence(_identity)
    rsa_public_key = factory.Sequence(str)
    rsa_private_key = factory.Sequence(lambda n: str(n) + '.pub')


class BuildFactory(Factory):
    FACTORY_FOR = Build

    id = factory.Sequence(_identity)
    gh_commit_author = 'aromanovich'
    gh_commit_message = 'ok'
    gh_commit_ref = 'master'
    status = 'enqueued'

    @factory.lazy_attribute
    def number(self):
        return len(self.project.builds.all()) + 1

    @factory.lazy_attribute
    def created_at(self):
        days = self.number
        return (datetime.datetime(2013, 11, 8, 20, 10, 25) +
                datetime.timedelta(days=days))

    @factory.lazy_attribute
    def gh_commit_sha(self):
        digest = hashlib.sha1()
        digest.update(str(self.id))
        return digest.hexdigest()


class JobFactory(Factory):
    FACTORY_FOR = Job

    id = factory.Sequence(_identity)


class TrackedFileFactory(Factory):
    FACTORY_FOR = TrackedFile

    path = factory.Sequence(u'path-{}.txt'.format)


class HookFactory(Factory):
    FACTORY_FOR = Hook

    id = factory.Sequence(_identity)
    gh_id = factory.Sequence(_identity)
    title = factory.Sequence(u'Hook {}'.format)
    build_script = './kozmic.sh'
    docker_image = 'ubuntu'


class HookCallFactory(Factory):
    FACTORY_FOR = HookCall

    id = factory.Sequence(_identity)

    @factory.lazy_attribute
    def gh_payload(self):
        return {}
