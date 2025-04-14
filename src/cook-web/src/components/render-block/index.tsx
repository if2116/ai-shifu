"use client"
import { useScenario } from '@/store';
import AI from './ai'
import SolidContent from './solid-content'
import { Select, SelectContent, SelectGroup, SelectItem, SelectTrigger, SelectValue } from '../ui/select';
import { Check, Trash2 } from 'lucide-react';
import { useState } from 'react';


const BlockMap = {
    ai: AI,
    solidcontent: SolidContent,
}

export const RenderBlockContent = ({ id, type, properties }) => {
    const { actions, blocks, blockContentTypes, blockContentState, currentOutline, blockUITypes, blockContentProperties, blockUIProperties } = useScenario();
    const [error, setError] = useState('')
    const onPropertiesChange = async (properties) => {
        console.log(id, properties)
        await actions.setBlockContentPropertiesById(id, properties)
        const p = {
            ...blockContentProperties,
            [id]: {
                ...blockContentProperties[id],
                ...properties
            }
        }
        setError('')
        if (type == 'ai' && properties.prompt == '') {
            setError('内容不能为空')
            return;
        } else if (type == 'solidcontent' && properties.content == '') {
            setError('内容不能为空')
            return;
        }
        actions.autoSaveBlocks(currentOutline, blocks, blockContentTypes, p, blockUITypes, blockUIProperties)
    }

    const onContentTypeChange = (id: string, type: string) => {
        const opt = ContentTypes.find(p => p.type === type);
        actions.setBlockContentTypesById(id, type)
        actions.setBlockContentPropertiesById(id, opt?.properties || {} as any, true)
    }
    const setIsEdit = (isEdit: boolean) => {
        actions.setBlockContentStateById(id, isEdit ? 'edit' : 'preview')
    }
    const onSave = async () => {
        setError('')
        // check if the block is empty
        const block = blocks.find((item) => item.properties.block_id == id);
        if (type == 'ai' && block && properties.prompt == '') {
            setError('内容不能为空')
            return;
        } else if (type == 'solidcontent' && block && properties.content == '') {
            setError('内容不能为空')
            return;
        }
        setIsEdit(false)
        await actions.saveBlocks();
    }
    const onRemove = async () => {
        actions.removeBlock(id);
    }
    const isEdit = blockContentState[id] == 'edit';
    const Ele = BlockMap[type]
    return (
        <div className='bg-[#F5F5F4] rounded-md'>
            {
                isEdit && (
                    <div className='rounded-t-md p-2 flex flex-row items-center py-1 justify-between'>
                        <Select
                            value={blockContentTypes[id]}
                            onValueChange={onContentTypeChange.bind(null, id)}
                        >
                            <SelectTrigger className="h-8 w-[120px]">
                                <SelectValue placeholder="请选择" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    {
                                        ContentTypes.map((item) => {
                                            return (
                                                <SelectItem key={item.type} value={item.type}>{item.name}</SelectItem>
                                            )
                                        })
                                    }
                                </SelectGroup>
                            </SelectContent>
                        </Select>
                        <div className='flex flex-row items-center'>
                            <div className='flex flex-row items-center px-2' onClick={onRemove}>
                                <Trash2 className='h-5 w-5 cursor-pointer' />
                            </div>
                            <div className='h-4 border-r border-[#D8D8D8] mx-1'></div>
                            <div className='flex flex-row items-center cursor-pointer px-2 ' onClick={onSave} >
                                <Check className='h-5 w-5 text-primary mr-2 shrink-0' />完成
                            </div>
                        </div>
                    </div>

                )
            }

            <div onDoubleClick={() => {
                setIsEdit(true)
            }}>
                <Ele
                    isEdit={isEdit}
                    properties={properties}
                    onChange={onPropertiesChange}
                />
            </div>
            {
                error && (
                    <div className='text-red-500 text-sm px-2 pb-2'>{error}</div>
                )
            }
        </div>

    )
}

export default RenderBlockContent;

export const ContentTypes = [
    {
        type: 'ai',
        name: 'AI块',
        properties: {
            "prompt": "",
            "profiles": [],
            "model": "",
            "temprature": "0.40",
            "other_conf": ""
        }
    },
    {
        type: 'solidcontent',
        name: '固定内容',
        properties: {
            "content": "",
            "profiles": [],
        }
    }
]
